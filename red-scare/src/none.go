package main

import "math"

func minDistance(dist []float64, sptSet []bool, n int) int {
	var minIndex int
	minimum := math.Inf(1)

	for i := 0; i < n; i++ {
		if dist[i] < minimum && !sptSet[i] {
			minimum = dist[i]
			minIndex = i
		}
	}
	return minIndex
}

func (g *graph) dijkstra(reds []bool, s int, t int, n int) int {

	dist := make([]float64, n)
	for i := range dist {
		dist[i] = math.Inf(1)
	}
	dist[s] = 0

	sptSet := make([]bool, n)

	for i := 0; i < n; i++ {

		x := minDistance(dist, sptSet, n)

		sptSet[x] = true

		for j := 0; j < n; j++ {
			if (*g)[i][j] > 0 && !sptSet[j] && dist[j] > dist[i]+float64((*g)[i][j]) {
				dist[j] = dist[i] + float64((*g)[i][j])
			}
		}

	}

	if dist[t] != math.Inf(1) {
		return int(dist[t])
	} else {
		return -1
	}

}
