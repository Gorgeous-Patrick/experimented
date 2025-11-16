use std::collections::HashMap;

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
    Run { stored_env: Option<String> },
    Init,
}

fn main() {
    let cli = Cli::parse();
    let mut map: HashMap<String, String> = HashMap::new();
    map.insert("Hello".to_string(), "100".to_string());
    match cli.command {
        Command::Init => init_store(None).unwrap(),
        Command::Run { stored_env } => {
            register_experiment(&map, None).unwrap();
            ()
        },
    }
}
