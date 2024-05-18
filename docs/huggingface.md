# HuggingFace 开源社区介绍

## 镜像

Huggignface官网的连接不稳定，下载大规模数据或模型时容易中断，找到一个[镜像站](https://hf-mirror.com/)。

只需要设置环境变量`HF_ENDPOINT`即可：

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

## 模型

### 仓库文件组成

以 [chatglm3-6b](https://huggingface.co/THUDM/chatglm3-6b/tree/main) 模型为例：
- xxx.safetensor：模型的权重文件，必须下载。safetensor 是 huggingface 默认且推荐的权重保存方式，相比 bin 等格式来说能够更好的处理异常。有的模型很大，可能分散在多个文件中，这种情况下 `model.safetensors.index.json` 文件也必须下载。
- model.safetensors.index.json：记录了多个权重文件的顺序索引。
- config.json：模型的配置文件，必须下载。huggignface 的模型都通过一个 config 来定义模型结构，详见源码介绍章节。
- xxx.bin：pytorch 模型权重文件。这是比较老的版本，建议使用 safetensor 版本的权重文件。对应的 index 文件同理。
- tokenizer.model：模型使用的分词器。
- tokenizer_config.json：分词器的配置文件。
- xxx.py：一些 huggingface 官方不支持的模型等，需要自行编写的模型、配置等相关文件。这些文件的编写必须遵循一定的原则，详见源码介绍章节。

### 模型下载方式

1. 手动下载：找到模型的仓库，手动下载 config、safetensor、tokenizer 等文件保存到本地，使用时通过下面的代码加载：
```python
from transformers import AutoModel, AutoModelForCausalLM
model = AutoModel.from_pretrained("/path/to/your/model")
# 某些针对特定任务的模型，比如语言模型
model = AutoModelForCausalLM.from_pretrained("/path/to/your/model")
```

2. from_pretrained 方法：推荐的下载方式，只需要模型的仓库名称。比如 chatglm 模型：
```python
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("THUDM/chatglm3-6b")
```

3. huggingface-cli：命令行直接运行类似下面的命令：
```bash
huggingface-cli download --resume-download gpt2 --local-dir gpt2
```

## 数据集

### 加载方式

1. load_dataset 方法：推荐使用，huggingface 的 datasets 库提供的加载方法，只需要数据集的仓库名。
```python
from datasets import load_dataset
dataset = load_dataset("wikitext")
```

2. huggingface-cli：命令行直接运行类似下面的命令：
```bash
huggingface-cli download --repo-type dataset --resume-download wikitext --local-dir wikitext
```

## 常用库

### transformers

源码链接：[transformers](https://github.com/huggingface/transformers)

Pytorch、Tensorflow、JAX 等框架的再次封装，实现了各种常见的深度学习模型，尤其是 transformer 类的模型。模型的代码文件具有极强的可读性，是了解大模型各种细节的优秀教材，比如 [llama](https://github.com/huggingface/transformers/tree/main/src/transformers/models/llama)。

模型的定义必须包含两个文件：configration_xxx.py 和 modeling_xxx.py，其中 xxx 表示模型名称。huggingface 所有的模型都必须有通过配置文件定义模型结构，这个配置包含了模型所有用到的参数信息。模型结构的定义必须包含在一个单一的 modeling_xxx.py 文件中，以防止其他人阅读源码时在各种文件之间跳转。

代码编写时往往会强调代码的复用性，尽可能减少重复代码的编写，但 transformers 库的设计却背道而驰。所有的模型定义必须包含在一个单一的文件中，这导致一些广泛使用的模块被反复复制在不同的文件中，比如 self-attention 的实现，这里体现了 transformers 库的设计理念，详见[知乎链接](https://zhuanlan.zhihu.com/p/648097305)。

### datasets

源码链接：[datasets](https://github.com/huggingface/datasets)

### accelerate

源码链接：[accelerate](https://github.com/huggingface/accelerate)

### peft

源码链接：[peft](https://github.com/huggingface/peft)

### gradio

源码链接：[gradio](https://github.com/gradio-app/gradio)

plus 版：[streamlit](https://github.com/streamlit/streamlit)