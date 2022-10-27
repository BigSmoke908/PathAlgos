use std::fs;
use std::fs::File;
use std::io::prelude::*;
use serde::{Deserialize, Serialize};


#[derive(Deserialize, Serialize)]
struct Buffer {
    maze: Vec<Vec<i32>>
}

struct Maze {
    m: Vec<Vec<i32>>,
    filepath: String
}

impl Maze {
    fn loadmaze(&mut self){
        let mut data: Buffer = serde_json::from_str(&self.read_file()).unwrap();
        self.m = data.maze;
    }

    fn savemaze(&self, maze: Vec<Vec<i32>>){
        let newmaze: Buffer = Buffer{maze: self.m};
        let data: String = serde_json::to_string(&newmaze).unwrap();
        fs::write(&self.filepath, data).expect("Unable to write file");
    }

    fn read_file(&self) -> String{
        let mut f = File::open(&self.filepath).expect("file not found");
        let mut content = String::new();
        f.read_to_string(&mut content).expect("something went wrong reading the file");
        return content;
    }
}

pub fn main(){
    let mut lab: Maze = Maze{m: vec![vec![0]], filepath: "s".to_string()};
    lab.filepath = "mazes/maze.json".to_string();
    lab.loadmaze();
    for y in 0..5{
        println!();
        for x in 0..5{
            print!("{}", lab.m[y][x]);
        }
    }
    lab.filepath = "mazes/newmaze.json".to_string();
    lab.savemaze(lab.m);
}
