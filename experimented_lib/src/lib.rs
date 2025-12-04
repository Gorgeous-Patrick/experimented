use std::{
    collections::HashMap,
    env,
    fs::{self, File},
    path::PathBuf,
};

use chrono::{DateTime, Utc};
use fs_extra::dir::CopyOptions;
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ExperimentedError {
    #[error("Experimented store not found.")]
    StoreNotFound,

    #[error("Cannot create folder.")]
    CreateFolder {
        #[from]
        source: std::io::Error,
    },

    #[error("Cannot copy folder.")]
    CopyFolder {
        #[from]
        source: fs_extra::error::Error,
    },

    #[error("Cannot dump json.")]
    JsonDump {
        #[from]
        source: serde_json::Error,
    },
}

fn find_store_helper(start_path: PathBuf) -> Result<PathBuf, ExperimentedError> {
    let store_name = ".ex";
    let mut base_path = start_path.as_path();
    loop {
        let store_path = base_path.join(store_name);
        if store_path.is_dir() {
            return Ok(store_path);
        }
        base_path = base_path.parent().ok_or(ExperimentedError::StoreNotFound)?;
    }
}

fn find_store(store_path_optional: Option<PathBuf>) -> Result<PathBuf, ExperimentedError> {
    return find_store_helper(store_path_optional.unwrap_or(env::current_dir().unwrap()));
}

#[derive(Serialize, Deserialize, Debug)]
struct ExperimentMetadata {
    start_time: DateTime<Utc>,
    vars: HashMap<String, String>,
}

fn init_store_helper(store_path: PathBuf) -> Result<(), ExperimentedError> {
    let store_name = ".ex";
    let store_path = store_path.join(store_name);
    fs::create_dir(store_path)?;
    Ok(())
}

pub fn init_store(store_path_optional: Option<PathBuf>) -> Result<(), ExperimentedError> {
    return init_store_helper(store_path_optional.unwrap_or(env::current_dir().unwrap()));
}

pub fn register_experiment(
    vars: &HashMap<String, String>,
    store_path_optional: Option<PathBuf>,
) -> Result<String, ExperimentedError> {
    let store_path = find_store(store_path_optional)?;
    let start_time: DateTime<Utc> = Utc::now();
    let experiment_path = store_path.join(start_time.to_string());
    fs::create_dir(&experiment_path)?;
    let config_json_path = experiment_path.join("config.json");
    let config_file = File::create_new(config_json_path)?;
    let config = ExperimentMetadata {
        start_time,
        vars: vars.clone(),
    };
    serde_json::to_writer(config_file, &config)
        .map_err(|source| ExperimentedError::JsonDump { source })?;
    Ok(start_time.to_string())
}

pub fn end_experiment(
    store_path_optional: Option<PathBuf>,
    result_path: PathBuf,
    start_time: String,
) -> Result<(), ExperimentedError> {
    let store_path = find_store(store_path_optional)?;
    let mut opts = CopyOptions::new();
    let destination_path = store_path.join(start_time).join("results");
    opts.copy_inside = true;
    let _ = fs_extra::dir::copy(result_path, destination_path, &opts)?;
    Ok(())
}
