# Audio-based Interaction
- We need to install `portaudio19-dev` first
  ```bash
  sudo apt install portaudio19-dev
  ```
- For best results, we can turn reasoning off. Here's the command to do the same for gemma4
  ```bash
  llama-server -m models/gemma4/gemma-4-E4B-it-Q4_K_M.gguf --jinja --reasoning-format auto --reasoning off --mmproj models/gemma4/mmproj-F16.gguf
  ```
