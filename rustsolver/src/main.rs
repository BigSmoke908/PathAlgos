use std::fs::File;
use std::io::prelude::*;
use serde_json;


struct Maze {
    name: String
}


fn main() {
    let file = "mazes/test.json";
    let data: serde_json::Value = serde_json::from_str(&read_file(file)).unwrap();
    println!("{:?}", data);
}


fn read_file(file:&str) -> String{
    let mut f = File::open(file).expect("file not found");
    let mut content = String::new();
    f.read_to_string(&mut content).expect("something went wrong reading the file");
    return content;
}
