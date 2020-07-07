#!/bin/bash

cd "$(dirname "$0")"

for f in */gtk-3.0/gtk.css; do
	echo "$f"

	IFS=$'\n'
	colors=$(grep 'define-color theme_' $f | grep -v \()
	for color in $colors; do

		# the color string (define-color keyword #XXX)
		color=${color/;/}              # | tr -d ";"
		color=${color/@define-color /} # | cut -c15-

		# the replace string ("#XXX" class="keyword")
		replace=$color
		regex='(theme_[a-z_]+) (#[a-zA-Z0-9]+)'
		while [[ $replace =~ $regex ]]; do
			class=${BASH_REMATCH[1]}
			replace="\"${BASH_REMATCH[2]}\" class=\"${BASH_REMATCH[1]}\""
		done

		# action
		for svg in $(dirname "$f")/img/*.svg; do
			echo " update $svg"
			sed -r -i 's/"#[a-zA-Z0-9]+" class="'$class'"/'$replace'/g' $svg
		done
	done
	unset IFS
done