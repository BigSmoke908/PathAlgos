use std::fs;
use std::fs::File;
use std::io::prelude::*;
use serde::{Deserialize, Serialize};
use serde_json;


// needed as a Step in between to make JSON parsing easier/possible
#[derive(Deserialize, Serialize)]
struct Buffer {
    maze: Vec<Vec<i32>>
}

// only used for reading/writing our maze to/from a file
#[derive(Clone)]
struct Maze {
    m: Vec<Vec<i32>>,
    filepath: String
}

impl Maze {
    fn loadmaze(&mut self){
        let mut data: Buffer = serde_json::from_str(&self.read_file()).unwrap();
        self.m = data.maze;
    }

    fn savemaze(&self){
        let new: Buffer = Buffer{maze: self.clone().m};
        let data: String = serde_json::to_string(&new).unwrap();
        fs::write(&self.filepath, data).expect("Unable to write file");
    }

    fn read_file(&self) -> String{
        let mut f = File::open(&self.filepath).expect("file not found");
        let mut content = String::new();
        f.read_to_string(&mut content).expect("something went wrong reading the file");
        return content;
    }
}


struct Generator {
    maze: Vec<Vec<i32>>,
    wall: i32,
    corridor: i32,
    searched: i32,
    x: i32,
    y:i32
}

impl Generator{
    // basically our constructor
    fn setup(mut self){
        self.maze = vec![vec![self.wall; ((self.x * 2) - 1) as usize]; ((self.y * 2) - 1) as usize];
        self.wall = 0;
        self.corridor = 1;
        self.searched = 2;
        self.x = 0;
        self.y = 0;
    }

    // checks, if a certain point is walkable
    fn p(self, x: i32, y: i32) -> bool{
        if (x * 2 < self.x) & (y * 2 < self.y){
            return self.maze[2 * y as usize][2 * x as usize] == self.corridor;
        }
        return false;
    }

    // sets a point to be walkable
    fn s(mut self, x: i32, y: i32){
        self.maze[y as usize * 2][x as usize * 2] = self.corridor;
    }

    // connects to points (as projected to the user) to be walkable
    fn c(mut self, x1: i32, y1: i32, x2: i32, y2: i32) {
        self.maze[y1 as usize * 2][x1 as usize * 2] = self.corridor;  // first point
        self.maze[y2 as usize * 2][x2 as usize * 2] = self.corridor;  // second point
        self.maze[y1 as usize + y2 as usize][x1 as usize + x2 as usize] = self.corridor;// point in between (the average)
    }

    fn printmaze(self){
        for i in 0..self.maze.len(){
            println!();
            for j in 0..self.maze[i].len(){
                print!("{}", self.maze[i][j]);
            }
        }
    }

    fn generate(mut self){
        println!("nö :)");
    }
}


pub fn main(){
    /*
    // Load Maze from file
    let mut lab: Maze = Maze{m: vec![vec![0]], filepath: "mazes/maze.json".to_string()};
    lab.loadmaze();

    // Save Maze to file
    lab.filepath = "mazes/newmaze.json".to_string();
    lab.savemaze();
    */
    let mut maze: Generator = Generator{
        maze: vec![vec![0]],
        wall: 0,
        corridor: 1,
        searched: 2,
        x: 0,
        y: 0
    };
    maze.x = 10;
    maze.y = 10;
    maze.setup();
    maze.printmaze();
}
