use globset::Glob;
use std::{collections::HashMap, env, path::Path};

use anyhow::Result;
use clap::{Parser, Subcommand};
use experimented::{init_store, register_experiment};

#[derive(Parser)]
#[command(name = "experimented")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    Init {
        path: Option<String>,
    },
    Run {
        path: Option<String>,
        env_vars: Option<String>,
    },
}

fn get_stored_env(stored_env_match: Option<String>) -> Result<HashMap<String, String>> {
    let vars = match stored_env_match {
        Some(env_match) => {
            let g = Glob::new(&env_match)?.compile_matcher();
            let mut vars = HashMap::new();
            for (key, value) in env::vars() {
                if g.is_match(&key) {
                    vars.insert(key, value);
                }
            }
            vars
        }
        None => {
            let mut vars = HashMap::new();
            for (key, value) in env::vars() {
                vars.insert(key, value);
            }
            vars
        }
    };
    Ok(vars)
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    match cli.command {
        Command::Init { path } => {
            init_store(path.map(|str| Path::new(&str).to_path_buf())).unwrap()
        }
        Command::Run { path, env_vars } => {
            let vars = get_stored_env(env_vars)?;
            register_experiment(&vars, path.map(|str| Path::new(&str).to_path_buf())).unwrap();
            ()
        }
    }
    Ok(())
}
