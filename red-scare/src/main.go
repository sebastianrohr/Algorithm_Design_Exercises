package main

import (
	"fmt"
)

type graph [][]int

func main() {
	var n, m, r int
	fmt.Scanln(&n, &m, &r)

	var s, t string
	fmt.Scanln(&s, &t)

	g := make(graph, n)
	for i := range g {
		g[i] = make([]int, n)
	}
	gBlack := make(graph, n)
	for i := range gBlack {
		gBlack[i] = make([]int, n)
	}
	gFew := make(graph, n)
	for i := range gFew {
		gFew[i] = make([]int, n)
		for j := range gFew[i] {
			gFew[i][j] = -1
		}
	}
	var nodes = make(map[string]int)
	reds := make([]bool, n)

	for i := 0; i < n; i++ {
		var name string
		var isRed string

		fmt.Scanln(&name, &isRed)
		nodes[name] = i

		if isRed == "*" {
			reds[i] = true
		}
	}

	for i := 0; i < m; i++ {
		var source, isDirected, target string
		fmt.Scanln(&source, &isDirected, &target)

		g[nodes[source]][nodes[target]] = 1
		if isDirected == "--" {
			g[nodes[target]][nodes[source]] = 1
		}

		if !reds[nodes[source]] && !reds[nodes[target]] {
			gBlack[nodes[source]][nodes[target]] = 1
			if isDirected == "--" {
				gBlack[nodes[target]][nodes[source]] = 1
			}
			gFew[nodes[source]][nodes[target]] = 0
			if isDirected == "--" {
				gFew[nodes[target]][nodes[source]] = 0
			}

		} else {
			gFew[nodes[source]][nodes[target]] = 1
			if isDirected == "--" {
				gFew[nodes[target]][nodes[source]] = 1
			}
		}
	}

	// case: None
	fmt.Println(gBlack.dijkstra(reds, nodes[s], nodes[t], n))

	// case: Some
	fmt.Println(g.some(reds, nodes[s], nodes[t], n))

	// case: Many

	// case: Few

	// case: Alternate
	fmt.Println(gFew.abfs(reds, nodes[s], nodes[t], n))
}
