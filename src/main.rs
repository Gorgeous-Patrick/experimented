use clap::{Parser, Subcommand};
use experimented::{greet};

#[derive(Parser)]
#[command(name = "experimented")]
struct Cli{
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    Greet {
        name: String
    },
    SomethingElse
}

fn main() {
    println!("Hello, world!");
    let cli = Cli::parse();
    match cli.command {
        Command::Greet { name } => greet(),
        Command::SomethingElse => {println!("SOMETHING")}
    }
}
