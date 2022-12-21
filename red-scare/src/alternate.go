package main

func (g *graph) abfs(reds []bool, s int, t int, n int) bool {

	visited := make([]bool, n)
	visited[s] = true

	queue := NewStack(n)
	queue.Push(s)

	var red bool
	if reds[s] {
		red = true
	} else {
		red = false
	}

	for !queue.IsEmpty() {

		element_interface, _ := queue.Pop()
		element := element_interface.(int)
		if element == t {
			return true
		}

		for i, v := range (*g)[element] {
			if v != 0 && !visited[i] && (red == reds[i]) {
				visited[i] = true
				queue.Push(i)
			}
		}
	}
	return false
}
