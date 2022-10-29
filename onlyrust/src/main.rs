use std::fs;
use std::fs::File;
use std::io::prelude::*;
use serde::{Deserialize, Serialize};
mod solve;


#[derive(Deserialize, Serialize)]
struct Buffer {
    maze: Vec<Vec<i32>>
}

impl Buffer{
    fn funnyfunc(&self){
        println!("{}", self.maze[0][0]);
    }
}


fn main() {
    // let file = "mazes/maze.json";
    // let data: Maze = serde_json::from_str(&read_file(file)).unwrap();
    // let maze = data.maze;
    // let maze = loadmaze(file);
    // savemaze("mazes/newmaze.json", maze);
    solve::main();
}


// Begin: Functions for loading and Saving a Maze---------------------------------------------------
// loads the maze which was saved as a JSON file (has to be the same structure as found in struct Maze
fn loadmaze(file:&str) -> Vec<Vec<i32>>{
    let data: Buffer = serde_json::from_str(&read_file(file)).unwrap();
    data.funnyfunc();
    return data.maze;
}


fn savemaze(file: &str, maze: Vec<Vec<i32>>){
    let newmaze: Buffer = Buffer{maze};
    let asstring: String = serde_json::to_string(&newmaze).unwrap();
    writetofile(file, asstring);
}


fn writetofile(file: &str, data: String){
    let _error = fs::write(file, data).expect("Unable to write file");
}


fn read_file(file:&str) -> String{
    let mut f = File::open(file).expect("file not found");
    let mut content = String::new();
    f.read_to_string(&mut content).expect("something went wrong reading the file");
    return content;
}
// End: Functions for loading and Saving a Maze-----------------------------------------------------
