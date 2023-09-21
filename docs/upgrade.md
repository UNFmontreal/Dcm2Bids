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

This major release includes many new features that unfortunately requires breaking
changes to configuration files.

### Changes to existing description and config file keys

Some _"keys"_ had to be renamed in order to better align with the BIDS
specification and reduce the risk of typos.

#### Description keys

|      key before      |        key now        |
| :------------------: | :-------------------: |
| **`dataType`**       | **`datatype`**        |
| **`modalityLabel`**  | **`suffix`**          |
| **`customLabels`**   | **`custom_entities`** |
| **`sidecarChanges`** | **`sidecar_changes`** |
| **`intendedFor`**    | **REMOVED**           |

#### Configuration file keys

|      key before      |        key now        |
| :------------------: | :-------------------: |
| **`caseSensitive`**  | **`case_sensitive`**  |
| **`defaceTpl`**      | **`post_op`**         |
| **`searchMethod`**   | **`search_method`**   |
| **DOES NOT EXIST**   | **`id`**              |
| **DOES NOT EXIST**   | **`extractor`**       |


### `sidecar_changes` : `intendedFor` and `id`

`intendedFor` has two major changes:

1. Since intendedFor has always been a sidecar change under the hood, it now
   must be nested in `sidecar_changes` and will be treated as such. intendedFor is not a description key anymore.
2. Instead of relying on the index of an image listed in the config file as used
   to be done in dcm2bids version <= 2.1.9, `intendedFor` now works with the newly created `id`
   key. The `id` key needs to be added to the image the index was referring to
   in <= 2.1.9. the value for `id` must be an arbitrary string but must
   corresponds to the value for `IntendedFor`.

Refer to the [id and IntendedFor documentation section](../how-to/create-config-file/#sidecar_changes-id-and-intendedfor) for more info.


### `custom_entities` and `extractors`

Please check the [custom_entities combined with extractors section](../how-to/use-advanced-commands/#custom_entities-combined-with-extractors) for more information.


### `post_op` now replaces `defaceTpl`

Since a couple of versions, defaceTpl has been removed. Instead of just putting it back, 
we also generalized the whole concept of post operation. After being converted into nifti 
and before moving it to the BIDS structure people can now apply whatever script they want to run on their data.

Please check the [post op section](../how-to/use-advanced-commands/#post_op) to get more info.
