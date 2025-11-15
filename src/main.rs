use clap::{Parser, Subcommand};
use experimented::run;

#[derive(Parser)]
#[command(name = "experimented")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    Run { stored_env: Option<String> },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Command::Run { stored_env } => run("h".to_string(), None).unwrap(),
    }
}
