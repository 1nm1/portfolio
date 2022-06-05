## Helm / K8s Cheat sheet

### Useful Resources

- https://helm.sh/docs/
- https://phoenixnap.com/kb/helm-commands-cheat-sheet

---

### Helm

- Add repo

  - ```
    helm repo add \
      --username ${USER} \
      --password ${PWD} \
      <NAME_OF_REPO> \
      <URL_OF_REPO>
    ```

- Update installed repos:

  - ```
    helm repo update
    ```

- List installed repos:

  - ```
    helm repo list
    ```

- List charts in repos:

  - ```
    helm search repo <NAME_OF_REPO>
    ```

- List versions / search for specific chart:

  - ```
    helm search repo <NAME_OF_REPO> -l | grep '<NAME_OF_CHART>'
    ```

- Show information about chart:

  - ```
    helm show chart <NAME_OF_REPO>/<NAME_OF_CHART>
    ```

- Show configuration values information about chart:

  - ```
    helm show values <NAME_OF_REPO>/<NAME_OF_CHART>
    ```

- Install helm chart to a K8s cluster:

  - ```
    helm install <NAME_OF_CLUSTER> <NAME_OF_REPO>/<NAME_OF_CHART> \
      --values ./path/to/values/as/yaml \
      --version <CHART_VERSION>
    ```

- Update a chart in a cluster:

  - ```
    helm upgrade <NAME_OF_CLUSTER> <NAME_OF_REPO>/<NAME_OF_CHART> \
      --install \
      --values ./path/to/values/as/yaml \
      --version <CHART_VERSION>
    ```

- View all install charts in all namespaces:
  - ```
    helm list -A
    ```
