## Helm / K8s Cheat sheet

### Helm

- Add repo

  - ```
    bash
    helm repo add \
     --username ${USER} \
     --password ${PWD} \
     ${REPO_NAME} \
     ${HEML_CHART_URL}
    ```

- Update installed repos:

  - ```
    bash
    helm repo update
    ```

- List installed repos:

  - ```
    bash
    helm repo list
    ```

- List charts in repos:

  - ```
    bash
    helm search repo starburstdata
    ```

- List versions / search for specific chart:
  - ```
    bash
    helm search repo starburstdata -l | grep '<NAME_OF_CHART>'
    ```
