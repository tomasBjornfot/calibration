package main

import (
	//"fmt"
	"os"
	"strconv"
)

func make_plane(start [3]float64, end [3]float64, dx float64, no_lines int) [][3]float64 {
	lines := make([][3]float64, 2*no_lines)
	for i := 0; i < no_lines; i++ {
		if i%2 == 0 {
			lines[2*i] = [3]float64{start[0] + float64(i)*dx, start[1], start[2]}
			lines[2*i+1] = [3]float64{end[0] + float64(i)*dx, end[1], end[2]}
		}
		if i%2 == 1 {
			lines[2*i+1] = [3]float64{start[0] + float64(i)*dx, start[1], start[2]}
			lines[2*i] = [3]float64{end[0] + float64(i)*dx, end[1], end[2]}
		}
	}
	return lines
}

func make_x_planes(start [3]float64, end [3]float64, dx float64, no_lines int, z_levels []float64) [][3]float64 {
	var x_plane = [][3]float64{}
	for i := 0; i < len(z_levels); i++ {
		_start := [3]float64{start[0], start[1], z_levels[i]}
		_end := [3]float64{end[0], end[1], z_levels[i]}
		plane := make_plane(_start, _end, dx, no_lines)
		if i == 0 {
			x_plane = plane
		} else {
			x_plane = merge_planes(plane, x_plane)
		}
	}
	return x_plane
}

func merge_planes(plane1 [][3]float64, plane2 [][3]float64) [][3]float64 {
	merged := make([][3]float64, len(plane1)+len(plane2))
	for i := 0; i < len(plane1); i++ {
		merged[i] = plane1[i]
	}
	for i := 0; i < len(plane2); i++ {
		merged[i+len(plane1)] = plane2[i]
	}
	return merged
}

func make_gcode(filename string, data [][3]float64) {
	s := ""
	for i := 0; i < len(data); i++ {
		x_string := strconv.FormatFloat(data[i][0], 'f', 1, 64)
		y_string := strconv.FormatFloat(data[i][1], 'f', 1, 64)
		z_string := strconv.FormatFloat(data[i][2], 'f', 1, 64)
		s += "G1"
		s += " X" + x_string
		s += " Y" + y_string
		s += " Z" + z_string
		s += " F1000"
		s += "\n"
	}
	myfile, _ := os.Create(filename)
	myfile.WriteString(s)
}

func main() {
	tr := 12.5 // tool_radius
	// z plane left
	start_zl := [3]float64{-275, 0, 40 + tr}
	end_zl := [3]float64{-275, 100, 40 + tr}
	zl_plane := make_plane(start_zl, end_zl, 5.0, 16)

	// z plane right
	start_zr := [3]float64{200, 0, 40 + tr}
	end_zr := [3]float64{200, 100, 40 + tr}
	zr_plane := make_plane(start_zr, end_zr, 5.0, 16)

	// x plane left
	z_levels := []float64{-20 + tr, -10 + tr, 0 + tr, 10 + tr, 20 + tr, 30 + tr}
	xl_plane := make_x_planes(start_zl, end_zl, 5.0, 8, z_levels)

	// x plane right
	start_xr := [3]float64{235, 0, 0}
	end_xr := [3]float64{235, 100, 0}
	xr_plane := make_x_planes(start_xr, end_xr, 5.0, 8, z_levels)

	point := make([][3]float64, 1)

	point[0] = [3]float64{-275, 0, 129}
	zl_plane = merge_planes(point, zl_plane)

	point[0] = [3]float64{-235, 0, 129}
	xl_plane = merge_planes(xl_plane, point)

	merge_l := merge_planes(zl_plane, xl_plane)
	merge_r := merge_planes(zr_plane, xr_plane)
	make_gcode("merge_l.gc", merge_l)
	make_gcode("merge_r.gc", merge_r)
	merge := merge_planes(merge_l, merge_r)
	make_gcode("merge.gc", merge)
}
