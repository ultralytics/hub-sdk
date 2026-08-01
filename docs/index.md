---
comments: false
description: Ultralytics HUB-SDK shutdown notice and Ultralytics Platform replacement resources.
keywords: Ultralytics Platform, HUB shutdown, HUB-SDK deprecated, Platform REST API
---

# Ultralytics HUB-SDK (Deprecated)

!!! warning "HUB-SDK shut down"

    Ultralytics HUB and HUB-SDK were deprecated and shut down on July 31, 2026. They have been fully replaced by [Ultralytics Platform](https://platform.ultralytics.com). The managed HUB-to-Platform migration was completed during Q2 2026 before the HUB shutdown.

Do not install or use HUB-SDK for new projects. It only communicates with retired HUB APIs and is not compatible with the Platform API. Legacy HUB API keys also do not work with Platform.

## Use Ultralytics Platform

Platform is the direct, substantially more capable HUB replacement and is free to start. It adds regional data residency, rich dataset uploads and statistics, annotation for all YOLO task types, Smart Annotation with SAM and YOLO models, cloud and remote training, browser prediction, all supported export formats, monitored endpoints in 42 global regions, and a full REST API.

The **$0/month Free plan** currently includes 100 GB of storage, unlimited public and private projects and datasets, up to 100 models, three concurrent cloud training jobs, three cloud deployments, Smart Annotation, all standard model exports, and community support. No credit card is required; compute-intensive operations use credits. See [Platform pricing](https://www.ultralytics.com/plans) for current limits.

1. Follow the [Platform quickstart](https://docs.ultralytics.com/platform/quickstart) to create an account.
2. Add new work and any local dataset or model copies directly to Platform. The managed HUB migration concluded in Q2 2026.
3. Create a new key under **Settings > API Keys** using the [Platform API key guide](https://docs.ultralytics.com/platform/account/api-keys).
4. Replace HUB-SDK integrations with the [Platform REST API](https://docs.ultralytics.com/platform/api).

The remaining pages on this site document historical source only. For current workflows, use the [Platform documentation](https://docs.ultralytics.com/platform).
