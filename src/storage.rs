use crate::{
    capi,
    components::macros::{cvt, impl_plain_old_dict},
};
use anyhow::{anyhow, Result};
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::{
    ffi::{CStr, CString},
    fmt::{Debug, Display},
    ptr::{null, null_mut},
};

#[pyclass]
#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub enum DimensionType {
    Space,
    Channel,
    Time,
    Other,
}

impl Default for DimensionType {
    fn default() -> Self {
        DimensionType::Space
    }
}

cvt!(DimensionType => capi::DimensionType,
    Space => DimensionType_DimensionType_Space,
    Channel => DimensionType_DimensionType_Channel,
    Time => DimensionType_DimensionType_Time,
    Other => DimensionType_DimensionType_Other
);

#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageDimension {
    #[pyo3(get, set)]
    #[serde(default)]
    pub(crate) name: Option<String>,

    #[pyo3(get, set)]
    #[serde(default)]
    pub(crate) kind: DimensionType,

    #[pyo3(get, set)]
    #[serde(default)]
    pub(crate) array_size_px: u32,

    #[pyo3(get, set)]
    #[serde(default)]
    pub(crate) chunk_size_px: u32,

    #[pyo3(get, set)]
    #[serde(default)]
    pub(crate) shard_size_chunks: u32,
}

impl Default for StorageDimension {
    fn default() -> Self {
        Self {
            name: Default::default(),
            kind: Default::default(),
            array_size_px: Default::default(),
            chunk_size_px: Default::default(),
            shard_size_chunks: Default::default(),
        }
    }
}

impl_plain_old_dict!(StorageDimension);

impl TryFrom<capi::StorageDimension> for StorageDimension {
    type Error = anyhow::Error;

    fn try_from(value: capi::StorageDimension) -> Result<Self, Self::Error> {
        let name = if value.name.nbytes == 0 {
            None
        } else {
            Some(
                unsafe { CStr::from_ptr(value.name.str_) }
                    .to_str()?
                    .to_owned(),
            )
        };

        Ok(Self {
            name,
            kind: value.kind.try_into()?,
            array_size_px: value.array_size_px,
            chunk_size_px: value.chunk_size_px,
            shard_size_chunks: value.shard_size_chunks,
        })
    }
}

#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageProperties {
    #[pyo3(get, set)]
    #[serde(default)]
    pub(crate) filename: Option<String>,

    #[pyo3(get, set)]
    #[serde(default)]
    pub(crate) external_metadata_json: Option<String>,

    /// Doesn't do anything right now. One day could be used for file-rollover.
    #[pyo3(get, set)]
    #[serde(default)]
    pub(crate) first_frame_id: u32,

    #[pyo3(get, set)]
    pub(crate) pixel_scale_um: (f64, f64),

    #[pyo3(get, set)]
    pub(crate) acquisition_dimensions: Vec<Py<StorageDimension>>,

    #[pyo3(get, set)]
    pub(crate) enable_multiscale: bool,
}

impl_plain_old_dict!(StorageProperties);

impl Default for StorageProperties {
    fn default() -> Self {
        Self {
            filename: Default::default(),
            external_metadata_json: Default::default(),
            first_frame_id: Default::default(),
            pixel_scale_um: (1., 1.), // Default to 1.0 um/pixel (square pixels)
            acquisition_dimensions: Default::default(),
            enable_multiscale: Default::default(),
        }
    }
}

impl TryFrom<capi::StorageProperties> for StorageProperties {
    type Error = anyhow::Error;

    fn try_from(value: capi::StorageProperties) -> Result<Self, Self::Error> {
        let filename = if value.filename.nbytes == 0 {
            None
        } else {
            Some(
                unsafe { CStr::from_ptr(value.filename.str_) }
                    .to_str()?
                    .to_owned(),
            )
        };
        let external_metadata_json = if value.external_metadata_json.nbytes == 0 {
            None
        } else {
            Some(
                unsafe { CStr::from_ptr(value.external_metadata_json.str_) }
                    .to_str()?
                    .to_owned(),
            )
        };

        let mut acquisition_dimensions: Vec<Py<StorageDimension>> = Default::default();
        for i in 0..value.acquisition_dimensions.size {
            acquisition_dimensions.push(Python::with_gil(|py| {
                Py::new(
                    py,
                    StorageDimension::try_from(unsafe {
                        *value.acquisition_dimensions.data.add(i)
                    })
                    .unwrap(),
                )
                .unwrap()
            }));
        }

        Ok(Self {
            filename,
            first_frame_id: value.first_frame_id,
            external_metadata_json,
            pixel_scale_um: (value.pixel_scale_um.x, value.pixel_scale_um.y),
            acquisition_dimensions,
            enable_multiscale: (value.enable_multiscale == 1),
        })
    }
}

impl Default for capi::String {
    fn default() -> Self {
        Self {
            str_: null_mut(),
            nbytes: Default::default(),
            is_ref: Default::default(),
        }
    }
}

impl Default for capi::PixelScale {
    fn default() -> Self {
        Self {
            x: Default::default(),
            y: Default::default(),
        }
    }
}

impl Default for capi::ImageShape_image_dims_s {
    fn default() -> Self {
        Self {
            channels: Default::default(),
            width: Default::default(),
            height: Default::default(),
            planes: Default::default(),
        }
    }
}

impl Default for capi::ImageShape_image_strides_s {
    fn default() -> Self {
        Self {
            channels: Default::default(),
            width: Default::default(),
            height: Default::default(),
            planes: Default::default(),
        }
    }
}

impl Default for capi::ImageShape {
    fn default() -> Self {
        Self {
            dims: Default::default(),
            strides: Default::default(),
            type_: Default::default(),
        }
    }
}

impl Display for capi::String {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let s = unsafe { CStr::from_ptr(self.str_) }.to_string_lossy();
        write!(f, "{}", s)
    }
}

/// StorageCapabilities
#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageCapabilities {
    #[pyo3(get)]
    chunking_is_supported: bool,

    #[pyo3(get)]
    sharding_is_supported: bool,

    #[pyo3(get)]
    multiscale_is_supported: bool,
}

impl_plain_old_dict!(StorageCapabilities);

impl Default for StorageCapabilities {
    fn default() -> Self {
        Self {
            chunking_is_supported: Default::default(),
            sharding_is_supported: Default::default(),
            multiscale_is_supported: Default::default(),
        }
    }
}

impl TryFrom<capi::StoragePropertyMetadata> for StorageCapabilities {
    type Error = anyhow::Error;

    fn try_from(value: capi::StoragePropertyMetadata) -> Result<Self, Self::Error> {
        Ok(Self {
            chunking_is_supported: value.chunking_is_supported == 1,
            sharding_is_supported: value.sharding_is_supported == 1,
            multiscale_is_supported: value.multiscale_is_supported == 1,
        })
    }
}

/// capi::StorageProperties
impl Default for capi::StorageProperties {
    fn default() -> Self {
        Self {
            filename: Default::default(),
            first_frame_id: Default::default(),
            external_metadata_json: Default::default(),
            pixel_scale_um: Default::default(),
            acquisition_dimensions: Default::default(),
            enable_multiscale: Default::default(),
        }
    }
}

impl TryFrom<&StorageProperties> for capi::StorageProperties {
    type Error = anyhow::Error;

    fn try_from(value: &StorageProperties) -> Result<Self, Self::Error> {
        let mut out: capi::StorageProperties = unsafe { std::mem::zeroed() };
        // Careful: x needs to live long enough
        let x = if let Some(filename) = &value.filename {
            Some(CString::new(filename.as_str())?)
        } else {
            None
        };
        let (filename, bytes_of_filename) = if let Some(ref x) = x {
            (x.as_ptr(), x.to_bytes_with_nul().len())
        } else {
            (null(), 0)
        };

        // Careful: y needs to live long enough
        let y = if let Some(metadata) = &value.external_metadata_json {
            Some(CString::new(metadata.as_str())?)
        } else {
            None
        };
        let (metadata, bytes_of_metadata) = if let Some(ref y) = y {
            (y.as_ptr(), y.to_bytes_with_nul().len())
        } else {
            (null(), 0)
        };

        // This copies the string into a buffer owned by the return value.
        if !unsafe {
            capi::storage_properties_init(
                &mut out,
                value.first_frame_id,
                filename,
                bytes_of_filename as _,
                metadata,
                bytes_of_metadata as _,
                capi::PixelScale {
                    x: value.pixel_scale_um.0,
                    y: value.pixel_scale_um.1,
                },
                value.acquisition_dimensions.len() as u8,
            ) == 1
        } {
            Err(anyhow::anyhow!("Failed to initialize storage properties."))
        } else if !unsafe {
            capi::storage_properties_set_enable_multiscale(&mut out, value.enable_multiscale as u8)
                == 1
        } {
            Err(anyhow::anyhow!("Failed acquire api status check"))
        } else {
            // initialize each dimension separately
            for (i, pydim) in value.acquisition_dimensions.iter().enumerate() {
                let dim = Python::with_gil(|py| -> PyResult<_> {
                    let storage_dim: StorageDimension = pydim.extract(py)?;
                    Ok(storage_dim)
                })?;

                // Careful: x needs to live long enough
                let x = if let Some(name) = &dim.name {
                    Some(CString::new(name.as_str())?)
                } else {
                    None
                };
                let (name, bytes_of_name) = if let Some(ref x) = x {
                    (x.as_ptr(), x.to_bytes_with_nul().len())
                } else {
                    (null(), 0)
                };

                if !unsafe {
                    capi::storage_properties_set_dimension(
                        &mut out,
                        i.try_into().unwrap(),
                        name,
                        bytes_of_name,
                        dim.kind.into(),
                        dim.array_size_px,
                        dim.chunk_size_px,
                        dim.shard_size_chunks,
                    ) == 1
                } {
                    return Err(anyhow::anyhow!("Failed to set storage dimension."));
                }
            }

            Ok(out)
        }
    }
}

/// capi::StorageProperties_storage_properties_dimensions_s
impl Default for capi::StorageProperties_storage_properties_dimensions_s {
    fn default() -> Self {
        Self {
            data: null_mut(),
            size: Default::default(),
        }
    }
}

/// capi::StorageDimension
impl Default for capi::StorageDimension {
    fn default() -> Self {
        Self {
            name: Default::default(),
            kind: Default::default(),
            array_size_px: Default::default(),
            chunk_size_px: Default::default(),
            shard_size_chunks: Default::default(),
        }
    }
}

/// capi::StoragePropertyMetadata
impl Default for capi::StoragePropertyMetadata {
    fn default() -> Self {
        Self {
            chunking_is_supported: Default::default(),
            sharding_is_supported: Default::default(),
            multiscale_is_supported: Default::default(),
        }
    }
}

impl TryFrom<&StorageCapabilities> for capi::StoragePropertyMetadata {
    type Error = anyhow::Error;

    fn try_from(value: &StorageCapabilities) -> Result<Self, Self::Error> {
        Ok(Self {
            chunking_is_supported: value.chunking_is_supported as u8,
            sharding_is_supported: value.sharding_is_supported as u8,
            multiscale_is_supported: value.multiscale_is_supported as u8,
        })
    }
}
