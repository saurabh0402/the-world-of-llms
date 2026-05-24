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

## The world is nothing but Hallucinations
- With thinking mode enabled, Gemma tends to hallucinate the tool response before it makes a call to the tool.
  - It does indeed make a tool call later but a lot of the times it isn't able to use the tool response to form the final result.
- One very important thing to be considered is that the small, local models start falling on their heads as the context gets even a little bigger - hallucinations starts, they can't use the data in the context, etc, etc. It's important to keep the contexts in check.
- Qwen's instruct model does not have thinking and for the simpler tasks that actually performs the best though because there's no thinking it seems a little less responsive.
- One very important thing to note - ***In the process of thinking, models tend to hallucinate a lot of stuff. So, for simpler tasks, don't use thinking at all. Use thinking models only when a lot of planning is needed and the task is pretty complex.***

# References
- [Quantization](https://huggingface.co/docs/optimum/en/concept_guides/quantization)
