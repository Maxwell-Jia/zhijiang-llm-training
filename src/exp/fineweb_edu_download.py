from collections import Counter
from datatrove.executor import LocalPipelineExecutor
from datatrove.pipeline.readers import ParquetReader
from datatrove.pipeline.filters import LambdaFilter, SamplerFilter
from datatrove.pipeline.writers import JsonlWriter

if __name__ == '__main__':
    pipeline_exec = LocalPipelineExecutor(
        pipeline=[
            ParquetReader("/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training/outputs/fineweb-edu-sample-100B/", glob_pattern="*.parquet"),
            JsonlWriter(output_folder="/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training/outputs/fineweb-edu/")
        ],
    )
    pipeline_exec.run()