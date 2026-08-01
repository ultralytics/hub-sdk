<div align="center">
  <a href="https://www.ultralytics.com/"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# Ultralytics HUB-SDK (Deprecated)

[Platform Docs](https://docs.ultralytics.com/platform) | [Platform REST API](https://docs.ultralytics.com/platform/api) | [Platform](https://platform.ultralytics.com)

</div>

> [!WARNING]
> Ultralytics HUB and HUB-SDK were deprecated and shut down on July 31, 2026. They have been fully replaced by [Ultralytics Platform](https://platform.ultralytics.com). HUB APIs and the HUB-to-Platform migration service are no longer available.

Do not install or use HUB-SDK for new projects. This package only communicates with the retired HUB APIs and is not compatible with the Platform API. Legacy HUB API keys also do not work with Platform.

## A More Capable Platform, Free to Start

Ultralytics Platform is the direct replacement for HUB and delivers a substantially more capable workflow in one workspace. The Free plan lets individuals get started without a subscription, with current plan limits and optional usage-based credits documented on Platform.

The **$0/month Free plan** currently includes 100 GB of storage, unlimited public and private projects and datasets, up to 100 models, three concurrent cloud training jobs, three cloud deployments, Smart Annotation, all standard model exports, and community support. No credit card is required; compute-intensive operations use credits.

| Capability | Ultralytics Platform improvement                                                                                                             |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Data       | Upload images, videos, ZIP, TAR, and NDJSON datasets with automatic validation, statistics, and regional data residency in the US, EU, or AP |
| Annotation | Label all YOLO task types with dedicated tools, custom pose skeletons, and Smart Annotation powered by SAM and YOLO models                   |
| Training   | Train on cloud GPUs or your own hardware while streaming real-time metrics, logs, and system statistics into organized projects              |
| Models     | Test predictions in the browser and export to 20 deployment formats, including ONNX, TensorRT, CoreML, LiteRT, and OpenVINO                  |
| Deployment | Launch dedicated, monitored inference endpoints in 42 global regions with scale-to-zero behavior                                             |
| Automation | Use new workspace-scoped Platform API keys and the full REST API for datasets, models, training, exports, and deployments                    |

## Use the Ultralytics Platform API

[Ultralytics Platform](https://platform.ultralytics.com) provides current programmatic access for dataset management, training, inference, exports, and deployments.

1. Follow the [Platform quickstart](https://docs.ultralytics.com/platform/quickstart) to create an account and select a data region.
2. Upload local copies of your datasets and model weights to Platform. The former automated HUB migration is no longer available.
3. Create a new key under **Settings > API Keys** and follow the [Platform API key guide](https://docs.ultralytics.com/platform/account/api-keys).
4. Replace HUB-SDK integrations with the documented [Platform REST API](https://docs.ultralytics.com/platform/api).

For remote training and metric streaming, install `ultralytics>=8.4.104`, set the new Platform API key, and use a `username/project` path:

```bash
pip install "ultralytics>=8.4.104"
export ULTRALYTICS_API_KEY="YOUR_PLATFORM_API_KEY"
yolo train model=yolo26n.pt data=coco.yaml epochs=100 project=username/project name=exp1
```

See the [Platform documentation](https://docs.ultralytics.com/platform) for current dataset, training, export, inference, and deployment workflows, or compare the current [Free, Pro, and Enterprise plans](https://www.ultralytics.com/plans).

## Repository Status

This repository and its source remain available as a historical reference only. The retired HUB service cannot be restored through repository issues or pull requests, and new HUB-SDK features are not accepted. For current product help and feedback, use the **Help** page in [Ultralytics Platform](https://platform.ultralytics.com), the [Platform documentation](https://docs.ultralytics.com/platform), or the [Ultralytics community forum](https://community.ultralytics.com/).

## License

See [LICENSE](LICENSE) for the license that applies to the historical source in this repository.
