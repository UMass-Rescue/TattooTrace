import path from 'node:path';
import { CLIPConfig, RecognitionConfig, TattoosRecognitionConfig } from '../smart-info/dto';

export const IMachineLearningRepository = 'IMachineLearningRepository';

// An interface that represents the input data structure expected by models that process visual information, such as images
export interface VisionModelInput {
  imagePath: string;
}

export interface TextModelInput {
  text: string;
}

export interface VideoModelInput {
  videoPath: string;
}

export interface BoundingBox {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export interface DetectFaceResult {
  imageWidth: number;
  imageHeight: number;
  boundingBox: BoundingBox;
  score: number;
  embedding: number[];
}

// Define the structure of the result of the detectTattoo model
// Our model returns images with tattoos, confidence scores
export interface RecognizeTattoosResult {
  filePath: string; // Path to the image
}

export enum ModelType {
  FACIAL_RECOGNITION = 'facial-recognition',
  CLIP = 'clip',
  TATTOOS_RECOGNITION = 'tattoos-recognition',
}

export enum CLIPMode {
  VISION = 'vision',
  TEXT = 'text',
}

// Specify possible types of model input, and can influence the behavior or processing pipeline of the model 
export enum MediaMode {
  IMAGE = 'image',
  VIDEO = 'video',
}

export interface IMachineLearningRepository {
  encodeImage(url: string, input: VisionModelInput, config: CLIPConfig): Promise<number[]>;
  encodeText(url: string, input: TextModelInput, config: CLIPConfig): Promise<number[]>;
  detectFaces(url: string, input: VisionModelInput, config: RecognitionConfig): Promise<DetectFaceResult[]>;
  recognizeTattoosInImage(url: string, input: VisionModelInput, config: TattoosRecognitionConfig): Promise<RecognizeTattoosResult>;
  recognizeTattoosInVideo(url: string, input: VideoModelInput, config: TattoosRecognitionConfig): Promise<RecognizeTattoosResult>;
}
