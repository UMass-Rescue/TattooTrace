import { ApiProperty } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsBoolean, IsEnum, IsNotEmpty, IsNumber, IsString, Max, Min } from 'class-validator';
import { Optional } from '../../domain.util';
import { CLIPMode, ModelType, MediaMode } from '../../repositories';

export class ModelConfig {
  @IsBoolean()
  enabled!: boolean;

  @IsString()
  @IsNotEmpty()
  modelName!: string;

  @IsEnum(ModelType)
  @Optional()
  @ApiProperty({ enumName: 'ModelType', enum: ModelType })
  modelType?: ModelType;
}

export class CLIPConfig extends ModelConfig {
  @IsEnum(CLIPMode)
  @Optional()
  @ApiProperty({ enumName: 'CLIPMode', enum: CLIPMode })
  mode?: CLIPMode;
}

export class RecognitionConfig extends ModelConfig {
  @IsNumber()
  @Min(0)
  @Max(1)
  @Type(() => Number)
  @ApiProperty({ type: 'number', format: 'float' })
  minScore!: number;

  @IsNumber()
  @Min(0)
  @Max(2)
  @Type(() => Number)
  @ApiProperty({ type: 'number', format: 'float' })
  maxDistance!: number;

  @IsNumber()
  @Min(1)
  @Type(() => Number)
  @ApiProperty({ type: 'integer' })
  minFaces!: number;
}

// Define the structure of data used to configure the detectTattoos model
export class TattoosRecognitionConfig extends ModelConfig {
  @IsNumber()
  @Min(0)
  @Max(1)
  @Type(() => Number)
  @ApiProperty({ type: 'number', format: 'float' }) // Define the structure of the score field
  minScore!: number; // The minimum confidence score for a tattoo to be considered a tattoo

  @IsEnum(MediaMode)
  @Optional()
  @ApiProperty({ enumName: 'MediaMode', enum: MediaMode }) // Define the structure of the mediaMode field
  mode?: MediaMode; // The type of media the model will be applied to

  // Add asset id to the config
  @IsString()
  @Optional()
  @ApiProperty({ type: 'string' })
  assetId?: string;
}
