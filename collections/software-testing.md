# Software testing and quality

A practical testing stack from fast local feedback to end-to-end and production-like validation.

| Layer | Recommended resources | What it covers |
|---|---|---|
| Unit | [Vitest](https://github.com/vitest-dev/vitest), [pytest](https://github.com/pytest-dev/pytest) | Fast logic and component-level checks. |
| Browser and E2E | [Playwright](https://github.com/microsoft/playwright), [Cypress](https://github.com/cypress-io/cypress) | Real-browser user flows and cross-browser behavior. |
| Integration | [Testcontainers](https://github.com/testcontainers/testcontainers-java) | Disposable databases and services in containers. |
| API | [Schemathesis](https://github.com/schemathesis/schemathesis) | Property-based testing generated from API schemas. |
| Accessibility | [axe-core](https://github.com/dequelabs/axe-core) | Automated accessibility rules and integrations. |
| Performance | [Grafana k6](https://github.com/grafana/k6) | Load, stress, and performance testing. |
| AI systems | [Promptfoo](https://github.com/promptfoo/promptfoo) | Prompt, model, agent, and red-team evaluations. |

Automation cannot prove correctness or accessibility on its own. Combine these tools with code review, exploratory testing, assistive-technology testing, and production monitoring.
