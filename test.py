import fasttext

def main():
    model = fasttext.load_model('/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training/outputs/astro-or-not-classifier/model.bin')

if __name__ == '__main__':
    # model = fasttext.load_model('/mnt/geogpt-gpfs/llm-course/home/jiaminghui/zhijiang-llm-training/outputs/astro-or-not-classifier/model.bin')
    main()