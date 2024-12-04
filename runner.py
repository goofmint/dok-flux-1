import torch
from diffusers import FluxPipeline
import argparse

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument(
    '--output',
    default='/opt/artifact',
    help='出力先ディレクトリを指定します。',
)
arg_parser.add_argument(
    '--prompt',
    default='',
    help='プロンプト',
)
arg_parser.add_argument(
    '--id',
    default='',
    help='タスクIDを指定します。',
)
arg_parser.add_argument(
    '--hf-token',
    default='',
    help='Hagging Faceのトークンを指定します。',
)
arg_parser.add_argument('--s3-bucket', help='S3のバケットを指定します。')
arg_parser.add_argument('--s3-endpoint', help='S3互換エンドポイントのURLを指定します。')
arg_parser.add_argument('--s3-secret', help='S3のシークレットアクセスキーを指定します。')
arg_parser.add_argument('--s3-token', help='S3のアクセスキーIDを指定します。')

args = arg_parser.parse_args()

output_path = f'{args.output}/output-{args.id}.png'

pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev",
                                    torch_dtype=torch.bfloat16,
                                    token=args.hf_token
)
pipe.to(torch.device("cuda"))  # deviceとしてCUDAを指定する

image = pipe(
    args.prompt,
    height=1024,
    width=1024,
    guidance_scale=3.5,
    output_type="pil",
    num_inference_steps=50,
    max_sequence_length=512,
    generator=torch.Generator("cuda").manual_seed(0)
).images[0]
image.save(output_path)
