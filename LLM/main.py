import argparse

import pandas as pd
from langchain import LLMChain, PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp
from tqdm import tqdm

from anonymization_prompt import anonymization_prompt_template


def main(model_path, input_path, output_path, column_name):
    df = pd.read_csv(input_path)

    if column_name not in df.columns:
        raise ValueError(
            f"Column {column_name} not found in the input CSV file. "
            f"Please specify the correct column name using the --column argument."
        )

    llm = LlamaCpp(
        model_path=model_path,
        n_parts=-1,
        n_batch=512,
        f16_kv=True,
        n_threads= 16,
        use_mmap=True,
        use_mlock=False,
        n_gpu_layers=128,
        n_ctx=4096,
        #n_gqa=0,
        temperature=0,
        max_tokens=4096*2,
        top_p=1,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        verbose=True,
        model_kwargs={"low_vram": False, "rms_norm_eps": 1.0e-06,},
    )

    anonymization_prompt = PromptTemplate(template=anonymization_prompt_template, input_variables=["prompt"])
    llm_chain = LLMChain(llm=llm, prompt=anonymization_prompt)

    print("Anonymization started...")
    for i, row in tqdm(df.iterrows()):
        df.loc[i, "anonymized"] = llm_chain.run(row[column_name])
    print("Anonymization completed...")

    df.to_csv(output_path, index=False)
    print(f"Anonymized reports saved to {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, help='Path to the GGUF model')
    parser.add_argument('--input', type=str, help='Path to the input CSV file')
    parser.add_argument('--output', type=str, help='Path to the output CSV file')
    parser.add_argument('--column', type=str, help='Column name containing the medical reports')

    args = parser.parse_args()

    main(args.model, args.input, args.output)
