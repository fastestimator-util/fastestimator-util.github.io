## Support Matrix

| FastEstimator  | Python | TensorFlow | PyTorch | CUDA |  Installation Instruction |
| -------------  | ------  | --------- | ------- | ---- | ----------- |
| Nightly  | 3.10-3.12  | 2.15.1 | 2.3.1 | 12.2.2 | master branch |
| 1.7 (recent stable) | 3.10-3.12  | 2.15.1 | 2.3.1 | 12.2 | [r1.7 branch](https://github.com/fastestimator/fastestimator/tree/r1.7) |
| 1.6  | 3.8-3.10  | 2.11.1 | 2.0.1 | 11.8 | [r1.6 branch](https://github.com/fastestimator/fastestimator/tree/r1.6) |
| 1.5  | 3.7-3.9  | 2.9.1 | 1.10.2 | 11.0 | [r1.5 branch](https://github.com/fastestimator/fastestimator/tree/r1.5) |
| 1.4  | 3.6-3.8  | 2.4.1 | 1.7.1 | 11.0 | [r1.4 branch](https://github.com/fastestimator/fastestimator/tree/r1.4) |
| 1.3  | 3.6-3.8  | 2.4.1 | 1.7.1 | 11.0 | [r1.3 branch](https://github.com/fastestimator/fastestimator/tree/r1.3) |
| 1.2  | 3.6-3.8  | 2.4.1 | 1.7.1 | 11.0 | [r1.2 branch](https://github.com/fastestimator/fastestimator/tree/r1.2) |
| 1.1  | 3.6-3.8  | 2.3.0 | 1.6.0 | 10.1 | [r1.1 branch](https://github.com/fastestimator/fastestimator/tree/r1.1) |


### 1. Install Dependencies

* Install TensorFlow
  * Linux:

      ```bash
      pip install tensorflow==2.15.1
      ```

  * Mac (M1/M2):
        Please follow this [installation guide](https://github.com/fastestimator/fastestimator/blob/master/installation_docs/mac_installation.md)

  * Windows:
        Please follow this [installation guide](https://github.com/fastestimator/fastestimator/blob/master/installation_docs/tensorflow_windows_installation.md)

* Install PyTorch
  * CPU:

      ```bash
      pip install --no-cache-dir torch==2.3.1+cpu torchvision==0.18.1+cpu torchaudio==2.3.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
      ```

  * GPU:

      ```bash
      pip install --no-cache-dir torch==2.3.1+cu121 torchvision==0.18.1+cu121 torchaudio==2.3.1+cu121 -f https://download.pytorch.org/whl/cu121/torch_stable.html
      ```

* Extra Dependencies:
  * Windows:
    * Install Build Tools for Visual Studio 2019 [here](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019).

    * Install latest Visual C++ redistributable [here](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads) and choose x86 for 32 bit OS, x64 for 64 bit OS.

  * Linux:

      ``` bash
      apt-get install libglib2.0-0 libsm6 libxrender1 libxext6
      ```

  * Mac:
    * Please follow this [installation guide](https://github.com/fastestimator/fastestimator/blob/master/installation_docs/mac_installation.md)

### 2. Install FastEstimator

* Stable:

    ``` bash
    pip install fastestimator
    ```

* Nightly (Linux/Mac):

    ``` bash
    pip install fastestimator-nightly
    ```

## Docker Hub

Docker containers create isolated virtual environments that share resources with a host machine. Docker provides an easy way to set up a FastEstimator environment. You can simply pull our image from [Docker Hub](https://hub.docker.com/r/fastestimator/fastestimator/tags) and get started:

* Stable:
  * GPU:

      ``` bash
      docker pull fastestimator/fastestimator:latest-gpu
      ```

  * CPU:

      ``` bash
      docker pull fastestimator/fastestimator:latest-cpu
      ```

* Nighly:
  * GPU:

      ``` bash
      docker pull fastestimator/fastestimator:nightly-gpu
      ```

  * CPU:

      ``` bash
      docker pull fastestimator/fastestimator:nightly-cpu
      ```