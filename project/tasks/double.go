package main

import (
	"encoding/json"
)

type Request struct {
    Data int
    Name string
}

func exec_task(arg string) string{

    req := Request{}

	json.Unmarshal([]byte(arg), &req)

	// double the data field
	req.Data = req.Data * 2

	// return the json string
	json, _ := json.Marshal(req)
	return string(json)
}