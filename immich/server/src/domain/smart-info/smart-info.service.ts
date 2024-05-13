import { ImmichLogger } from '@app/infra/logger';
import { Inject, Injectable, BadRequestException } from '@nestjs/common';
import { usePagination } from '../domain.util';
import { IBaseJob, IEntityJob, JOBS_ASSET_PAGINATION_SIZE, JobName, QueueName } from '../job';
import {
  IAccessRepository,
  DatabaseLock,
  IAssetRepository,
  IDatabaseRepository,
  IJobRepository,
  IMachineLearningRepository,
  ISmartInfoRepository,
  ISystemConfigRepository,
  WithoutProperty,
  MediaMode,
} from '../repositories';
import { SystemConfigCore } from '../system-config';
import { AccessCore, Permission } from '../access';
import { AuthDto } from '../auth';
import { TattoosRecognitionResponseDto } from './dto/smart-info.dto';
import { AssetType } from '@app/infra/entities';
import e from 'express';

@Injectable()
export class SmartInfoService {
  private configCore: SystemConfigCore;
  private logger = new ImmichLogger(SmartInfoService.name);
  private access: AccessCore;

  constructor(
    @Inject(IAccessRepository) accessRepository: IAccessRepository,
    @Inject(IAssetRepository) private assetRepository: IAssetRepository,
    @Inject(IDatabaseRepository) private databaseRepository: IDatabaseRepository,
    @Inject(IJobRepository) private jobRepository: IJobRepository,
    @Inject(IMachineLearningRepository) private machineLearning: IMachineLearningRepository,
    @Inject(ISmartInfoRepository) private repository: ISmartInfoRepository,
    @Inject(ISystemConfigRepository) configRepository: ISystemConfigRepository,
  ) {
    this.access = AccessCore.create(accessRepository);
    this.configCore = SystemConfigCore.create(configRepository);
  }

  async init() {
    await this.jobRepository.pause(QueueName.SMART_SEARCH);

    await this.jobRepository.waitForQueueCompletion(QueueName.SMART_SEARCH);

    const { machineLearning } = await this.configCore.getConfig();

    await this.databaseRepository.withLock(DatabaseLock.CLIPDimSize, () =>
      this.repository.init(machineLearning.clip.modelName),
    );

    await this.jobRepository.resume(QueueName.SMART_SEARCH);
  }

  async handleQueueEncodeClip({ force }: IBaseJob) {
    const { machineLearning } = await this.configCore.getConfig();
    if (!machineLearning.enabled || !machineLearning.clip.enabled) {
      return true;
    }

    const assetPagination = usePagination(JOBS_ASSET_PAGINATION_SIZE, (pagination) => {
      return force
        ? this.assetRepository.getAll(pagination)
        : this.assetRepository.getWithout(pagination, WithoutProperty.SMART_SEARCH);
    });

    for await (const assets of assetPagination) {
      await this.jobRepository.queueAll(
        assets.map((asset) => ({ name: JobName.SMART_SEARCH, data: { id: asset.id } })),
      );
    }

    return true;
  }

  async handleEncodeClip({ id }: IEntityJob) {
    const { machineLearning } = await this.configCore.getConfig();
    if (!machineLearning.enabled || !machineLearning.clip.enabled) {
      return true;
    }

    const [asset] = await this.assetRepository.getByIds([id]);
    if (!asset.resizePath) {
      return false;
    }

    const clipEmbedding = await this.machineLearning.encodeImage(
      machineLearning.url,
      { imagePath: asset.resizePath },
      machineLearning.clip,
    );

    if (this.databaseRepository.isBusy(DatabaseLock.CLIPDimSize)) {
      this.logger.verbose(`Waiting for CLIP dimension size to be updated`);
      await this.databaseRepository.wait(DatabaseLock.CLIPDimSize);
    }

    await this.repository.upsert({ assetId: asset.id }, clipEmbedding);

    return true;
  }

  async handleRecognizeTattoos(auth: AuthDto, id: string): Promise<TattoosRecognitionResponseDto> {

    let response: TattoosRecognitionResponseDto = {id: id, filePath: '', mediaMode: MediaMode.IMAGE};

    await this.access.requirePermission(auth, Permission.ASSET_READ, id);

    const { machineLearning } = await this.configCore.getConfig();
    if (!machineLearning.enabled || !machineLearning.tattoosRecognition.enabled){
      throw new BadRequestException('Machine learning is disabled');
    }

    const asset = await this.assetRepository.getById(id);

    if (!asset) {
      throw new BadRequestException('Asset not found');
    }
    //if the asset doesn't have a resize path or original path, it can't be processed
    if (!asset.resizePath && !asset.originalPath) {
      throw new BadRequestException('Asset has no image or video file path');
    }
    // if (!asset.resizePath) {
    //   throw new BadRequestException('Asset has no image file path');
    // }

    if (asset.type === AssetType.VIDEO && asset.originalPath) {
      const recognizedTattoos = await this.machineLearning.recognizeTattoosInVideo(
        machineLearning.url,
        { videoPath: asset.originalPath },
        { ...machineLearning.tattoosRecognition,
          assetId: id,
        }
      );

      response = {
        id: id,
        filePath: recognizedTattoos.filePath,
        mediaMode: MediaMode.VIDEO,
      };
    }
    else if (asset.type === AssetType.IMAGE && asset.resizePath) {
      const recognizedTattoos = await this.machineLearning.recognizeTattoosInImage(
        machineLearning.url,
        { imagePath: asset.resizePath },
        { ...machineLearning.tattoosRecognition,
          assetId: id,
        }
      );

      response = {
        id: id,
        filePath: recognizedTattoos.filePath,
        mediaMode: MediaMode.IMAGE,
      };
    }
    // const detectedWeapons = await this.machineLearning.detectWeapons(
    //   machineLearning.url,
    //   { imagePath: asset.resizePath },
    //   { ...machineLearning.weaponsDetection,
    //     mode: asset.type === AssetType.VIDEO ? MediaMode.VIDEO : MediaMode.IMAGE
    //   },
    // );

    // const response = {
    //   id: id,
    //   data: detectedWeapons.map((weapon) => ({
    //     image: weapon.image,
    //     score: weapon.score,
    //   })),
    // };

    return response;
  }
}
