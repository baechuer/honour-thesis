# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (2089 skills)
- Reranker: `qwen`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 80.0% |
| Acceptable top-1 accuracy | 100.0% |
| Top-3 recall | 100.0% |
| Top-5 recall | 100.0% |
| Acceptable top-5 recall | 100.0% |
| MRR | 0.900 |
| Non-main top-1 | 20.0% |
| Approx selector-visible tokens | 1119733 |

## API Usage Estimate

- Embedding API calls made in this run: 114
- Embedding cache hits: 1005
- Approx uncached embedding input tokens: 569418
- Rerank API calls made in this run: 5
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 54161

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, api-ops-quality-auditor, api-ops-acceptance-test-builder, public-api-design-principles |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 2 | 1 | `api-integration-planner` | acceptable | api-integration-planner, external-api-integration-planner, api-ops-acceptance-test-builder, api-ops-scenario-planner, api-ops-timeline-builder |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, events-ops-acceptance-test-builder, invoice-payment-checker, receipt-extractor |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, sre-ops-dependency-mapper, platform-ops-dependency-mapper, cloud-ops-dependency-mapper |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, public-office-subscription-management, database-ops-monitoring-plan-builder, customer-success-ops-normalizer |
