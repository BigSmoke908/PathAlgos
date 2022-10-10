use std::fs::File;
use std::io::prelude::*;
use serde_json;

fn main() {
    let rawdata = read_file("mazes/maze.json");
    let data: serde_json::Value = serde_json::from_str(&rawdata).expect("JSON was not well-formatted");
    let x = 5;
    let y = 5;
    let data = &data[0];

    for row in 0..x{
        println!();
        for pixel in 0..y{
            print!("{}", &data[row][pixel]);
        }
    }
}


fn read_file(file:&str) -> String{
    let mut f = File::open(file).expect("file not found");

    let mut contents = String::new();
    f.read_to_string(&mut contents).expect("something went wrong reading the file");

    return contents;
}
