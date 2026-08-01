<div align="center">
  <a href="https://www.ultralytics.com/"><img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320" alt="Ultralytics logo"></a>

# Ultralytics HUB-SDK (Deprecated)

[Platform Docs](https://docs.ultralytics.com/platform) | [Platform REST API](https://docs.ultralytics.com/platform/api) | [Platform](https://platform.ultralytics.com)

</div>

> [!WARNING]
> Ultralytics HUB and HUB-SDK were deprecated and shut down on July 31, 2026. They have been fully replaced by [Ultralytics Platform](https://platform.ultralytics.com). The managed HUB-to-Platform migration was completed during Q2 2026 before the HUB shutdown.

Do not install or use HUB-SDK for new projects. This package only communicates with the retired HUB APIs and is not compatible with the Platform API. Legacy HUB API keys also do not work with Platform.

## A More Capable Platform, Free to Start

Ultralytics Platform is the direct replacement for HUB and delivers a substantially more capable workflow in one workspace. A meaningful Free plan lets individuals get started, while [Platform pricing](https://www.ultralytics.com/pricing) remains the source of truth for current limits and optional usage-based credits.

| Capability | Ultralytics Platform improvement                                                                                      |
| ---------- | --------------------------------------------------------------------------------------------------------------------- |
| Data       | Upload and validate rich computer vision datasets with built-in statistics and workspace organization                 |
| Annotation | Label supported YOLO annotation task types with dedicated tools and Smart Annotation powered by SAM and YOLO models   |
| Training   | Train on cloud GPUs or your own hardware while streaming metrics, logs, and system statistics into organized projects |
| Models     | Test predictions in the browser and export models to supported deployment formats                                     |
| Deployment | Launch and monitor dedicated inference endpoints                                                                      |
| Automation | Use workspace-scoped Platform API keys and the REST API for datasets, models, training, exports, and deployments      |

## Use the Ultralytics Platform API

[Ultralytics Platform](https://platform.ultralytics.com) provides current programmatic access for dataset management, training, inference, exports, and deployments.

1. Sign in to your migrated Platform account, or follow the [Platform quickstart](https://docs.ultralytics.com/platform/quickstart) to create one if you are new.
2. Add new work and any local dataset or model copies directly to Platform. The managed HUB migration concluded in Q2 2026.
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
