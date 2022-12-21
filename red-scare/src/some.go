package main

func (g *graph) dfs(s int, t int, n int, parent *[]int) bool {
	visited := make([]bool, n)
	visited[s] = true

	queue := NewStack(n)
	queue.Push(s)

	for !queue.IsEmpty() {

		element_interface, _ := queue.Pop()
		element := element_interface.(int)
		if element == t {
			return true
		}

		for i, v := range (*g)[element] {
			if v != 0 && !visited[i] {
				visited[i] = true
				(*parent)[i] = element
				queue.Push(i)
			}
		}
	}
	return false
}

func (g *graph) some(reds []bool, s int, t int, n int) bool {

	for i, v := range reds {
		if v {
			if g.dfs(s, i, n) && g.dfs(i, t, n) {
				return true
			}
		}
	}
	return false
}
