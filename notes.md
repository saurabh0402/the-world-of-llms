# Notes
## Running Gemma4
- Running Gemma4 on Ollama is failing with the following error
  ```
  Error: 500 Internal Server Error: unable to load model: /usr/share/ollama/.ollama/models/blobs/sha256-da6cde635109e22692b6ccb3a6075e44a9e2f7e6c698383b51a58aa9b8011de8
  ```
- This is because version `0.24.0` (the current latest one) does not support it. The support is coming but until then here's how we can run it.
- Pull the model
  ```bash
  ollama pull hf.co/unsloth/gemma-4-E4B-it-GGUF:Q4_K_M 
  ```
- Check the Modelfile for the model
  ```bash
  ollama show --modelfile hf.co/unsloth/gemma-4-E4B-it-GGUF:Q4_K_M
  ```
- Copy the content and create a new file called `Modelfile` and paste the content.
- Comment out the second `FROM` statement.
- Build the model
  ```bash
  ollama create gemma4:q4 -f Modelfile
  ```
- That's it, run the model.
  ```bash
  ollama run gemma4:q4
  ```

## Why Gemma Why?
- Gemma uses role `tool_response` for tool's response whereas most other models use `tool`.
- Langchain does not support setting custom `tool_response` role and therefore we were unable to get it to work fully.

# References
- [Quantization](https://huggingface.co/docs/optimum/en/concept_guides/quantization)
