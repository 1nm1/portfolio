### Helpful resources

- Terraform explained in 15 mins | Terraform Tutorial for Beginners

  - https://www.youtube.com/watch?v=l5k1ai_GBDE

- Terraform Course - Automate your AWS cloud infrastructure

  - https://www.youtube.com/watch?v=SLB_c_ayRMo

- GCP
  - https://registry.terraform.io/providers/hashicorp/google/latest/docs
  - https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/gcp-get-started
  - https://stackoverflow.com/questions/66281882/how-can-i-get-terraform-init-to-run-on-my-apple-silicon-macbook-pro-for-the-go

### General notes

- 2 input sources

  - TF-config
  - State

- Use TF_LOG=DEBUG to help address issues

Main commands:

- init Prepare your working directory for other commands
- validate Check whether the configuration is valid
- plan Show changes required by the current configuration
- apply Create or update infrastructure
- destroy Destroy previously-created infrastructure

All other commands:

- console Try Terraform expressions at an interactive command prompt
- fmt Reformat your configuration in the standard style
- force-unlock Release a stuck lock on the current workspace
- get Install or upgrade remote Terraform modules
- graph Generate a Graphviz graph of the steps in an operation
- import Associate existing infrastructure with a Terraform resource
- login Obtain and save credentials for a remote host
- logout Remove locally-stored credentials for a remote host
- output Show output values from your root module
- providers Show the providers required for this configuration
- refresh Update the state to match remote systems
- show Show the current state or a saved plan
- state Advanced state management
- taint Mark a resource instance as not fully functional
- untaint Remove the 'tainted' state from a resource instance
- version Show the current Terraform version
- workspace Workspace management
