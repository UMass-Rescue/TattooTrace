import { AuthDto, TattoosRecognitionResponseDto, SmartInfoService } from '@app/domain';
import { Controller, Get, Param } from '@nestjs/common';
import { ApiTags } from '@nestjs/swagger';
import { Auth, Authenticated } from '../app.guard';
import { UseValidation } from '../app.utils';
import { UUIDParamDto } from './dto/uuid-param.dto';

@ApiTags('TattoosRecognize')
@Controller('tattoos-recognize')
@Authenticated()
@UseValidation()
export class TattoosRecognizeController {
  constructor(private service: SmartInfoService) {}

  @Get(':id')
  getTattoosRecognize(@Auth() auth: AuthDto, @Param() { id }: UUIDParamDto): Promise<TattoosRecognitionResponseDto> {
    return this.service.handleRecognizeTattoos(auth, id);
  }
  
}

