## Helm / K8s Cheat sheet

There are a lot of helm and k8s commands and likewise a lot of published cheat sheets (some list in resources below). These are the commands I tend to use the most.

### Useful Resources

- https://helm.sh/docs/
- https://phoenixnap.com/kb/helm-commands-cheat-sheet
- https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands
- https://kubernetes.io/docs/reference/kubectl/cheatsheet/

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

---

### Kubernetes

| Description              | Command                                             | Notes                                      |
| ------------------------ | --------------------------------------------------- | ------------------------------------------ |
| View Pod Status          | kubectl get pods                                    | add --watch to print live status           |
| Shell into coordinator   | kubectl exec -it <COORD_POD> -c coordinator -- bash |                                            |
| Shell into pod (generic) | kubectl exec -it <POD> -- bash                      |                                            |
| Get pod logs             | kubectl logs <POD>                                  |                                            |
| Get coordinator pod logs | kubectl logs <POD> -c coordinator                   |                                            |
| Create a secret          | kubectl create secret generic <SECRET_NAME>         | Sources can vary (i.e. from file or other) |
| List secrets             | kubectl get secrets                                 |                                            |
| Move local file to pod   | kubectl cp /path/to/local/file <POD>:/pod/path      |                                            |
| Port forward             | kubectl port-forward pod/<COORD_POD> 8443:8443      |                                            |
| List details on ingress  | kubectl describe ing <NAME_OF_INGRESS>              |                                            |
| List general info on ing | kubectl get ing                                     |                                            |
