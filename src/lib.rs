use std::{
    env,
    error::Error,
    path::{self, Path, PathBuf},
};

use thiserror::Error;

#[derive(Error, Debug)]
pub enum ExperimentedError {
    #[error("Experimented store not found.")]
    StoreNotFound,
}

fn find_store(start_path: PathBuf) -> Result<PathBuf, ExperimentedError> {
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
pub fn run(
    stored_env: String,
    store_path_optional: Option<PathBuf>,
) -> Result<(), ExperimentedError> {
    let store_path = find_store(store_path_optional.unwrap_or(env::current_dir().unwrap()))?;
    Ok(())
}
