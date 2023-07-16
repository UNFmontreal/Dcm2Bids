# How to upgrade

Upgrade to the latest version using your favorite method.

=== "conda"

    ```bash hl_lines="2"
    sam:~$ conda activate dcm2bids-dev
    sam:~$ conda update dcm2bids
    ```

=== "pip"

    ```bash
    sam:~$ pip install --upgrade --force-reinstall dcm2bids
    ```

!!! tip "Binary executables now available"

    Tired of dealing with virtual envs in Python? You can now download executables
    directly from GitHub and use them right away. See [Install dcm2bids](../get-started/install/#installing-binary-executables) for more info.

## Upgrading from 2.x to 3.x

This major release includes many new features that unfortunaly requires breaking
changes to configuration files.

### _"key"_ changes

#### Changes to existing keys

Some _"keys"_ had to be renamed in order to better align with the BIDS
specification and reduce the risk of typos.

|      key before      |        key now        |
| :------------------: | :-------------------: |
|    **`dataType`**    |    **`datatype`**     |
| **`modalityLabel`**  |     **`suffix`**      |
| **`customEntities`** | **`custom_entities`** |
| **`sidecarChanges`** | **`sidecar_changes`** |
|  **`searchMethod`**  |  **`search_method`**  |
|   **`defaceTpl`**    |     **`post_op`**     |
| **`caseSensitive`**  | **`case_sensitive`**  |

#### `sidecar_changes`

#### `intendedFor` and `id`

`intendedFor` has two major changes:

1. Since intendedFor has always been a sidecar change under the hood, it now
   must be nested in `sidecar_changes` and will be treated as such.
2. Instead of relying on the index of an image listed in the config file as used
   to be done in <= 2.1.9, `intendedFor` now works with the newly created `id`
   key. The `id` key needs to be added to the image the index was referring to
   in <= 2.1.9. the value for `id` must be an arbitrary string but must
   corresponds to the value for `intendedFor`.

Refer to the [id documentation section][config-file-id] for more info.

#### `post_op` now replaces `defaceTpl`

### new features

`dup_method`

[config-file-id]:
  ../how-to/create-config-file/#sidecar_changes-id-and-intendedfor
