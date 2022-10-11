use std::fs::File;
use std::io::prelude::*;
use serde_json;

fn main() {
    let file = "mazes/maze.json";
    let data: serde_json::Value = serde_json::from_str(&read_file(file)).expect("JSON was not well-formatted");
    let mut finalData = vec![];
    let x = 5;
    let y = 5;

    for row in 0..x{
        finalData.push(vec![]);
        for pixel in 0..y{
            finalData[row].push(&data[row][pixel]);
        }
    }

    for row in 0..x{
        println!();
        for pixel in 0..y{
            print!("{}", finalData[row][pixel]);
        }
    }
}


fn read_file(file:&str) -> String{
    let mut f = File::open(file).expect("file not found");
    let mut content = String::new();
    f.read_to_string(&mut content).expect("something went wrong reading the file");
    return content;
}
