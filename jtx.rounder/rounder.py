#!/usr/bin/python3
'''
Rounder 0.4
Based in deprecated "Path Rounder 0.2"
Based in  radiusrand script from Aaron Spike and make it by Jabier Arraiza, 
jabier.arraiza@marker.es
Copyright (C) 2005 Aaron Spike, aaron@ekips.org

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''
import inkex


class svgRounder(inkex.Effect):
    def __init__(self):
        super().__init__()
        self.arg_parser.add_argument("--p", "--precision",
            type=int, dest="precision", default=3,
            help="Precision")
        self.arg_parser.add_argument("-c", "--ctrl",
            type=inkex.Boolean, dest="ctrl", default=False,
            help="Round node handles")
        self.arg_parser.add_argument("-a", "--along",
            type=inkex.Boolean, dest="along", default=True,
            help="Move handles following node movement")
        self.arg_parser.add_argument("--half",
            type=inkex.Boolean, dest="half", default=False,
            help="Allow round to half if nearest")
        self.arg_parser.add_argument("-p", "--paths",
            type=inkex.Boolean, dest="paths", default=True,
            help="Affect to paths")
        self.arg_parser.add_argument("-w", "--widthheight",
            type=inkex.Boolean, dest="widthheight", default=False,
            help="Affect to width and height of objects")
        self.arg_parser.add_argument("-x", "--position",
            type=inkex.Boolean, dest="position", default=False,
            help="Affect to position of objects")
        self.arg_parser.add_argument("-s", "--strokewidth",
            type=inkex.Boolean, dest="strokewidth", default=False,
            help="Affect to stroke width of objects")
        self.arg_parser.add_argument("-o", "--opacity",
            type=inkex.Boolean, dest="opacity", default=False,
            help="Affect to global opacity of objects")
        self.arg_parser.add_argument("--strokeopacity",
            type=inkex.Boolean, dest="strokeopacity", default=False,
            help="Affect to stroke opcacity of objects")
        self.arg_parser.add_argument("--fillopacity",
            type=inkex.Boolean, dest="fillopacity", default=False,
            help="Affect to fill opcacity of objects")

    def roundFloat(self, n):
        if self.options.half:
            multiplier = 10 ** self.options.precision
            n *= multiplier
            n = round(n * 2) / 2
            return n / multiplier
        return round(n,  self.options.precision)
 
    def roundUnit(self, value):
        value, unit = inkex.units.parse_unit(value, '')
        value = self.roundFloat(value)
        return f'{value}{unit}'
        
    def roundPoint(self, p):
        x = self.roundFloat(p[0])
        y = self.roundFloat(p[1])
        return [x - p[0], y - p[1]]
    
    def path_round_it(self, node):
        if node.tag == inkex.addNS('g', 'svg'):
            for e in node:
                self.path_round_it(e)
        elif node.tag == inkex.addNS('path', 'svg'):
            d = node.get('d')
            p = inkex.CubicSuperPath(d)
            for subpath in p:
                for csp in subpath:
                    delta = self.roundPoint(csp[1])
                    if self.options.along:
                        csp[0][0] += delta[0] 
                        csp[0][1] += delta[1] 
                    csp[1][0] += delta[0] 
                    csp[1][1] += delta[1] 
                    if self.options.along:
                        csp[2][0] += delta[0] 
                        csp[2][1] += delta[1] 
                    if self.options.ctrl:
                        delta = self.roundPoint(csp[0])
                        csp[0][0] += delta[0] 
                        csp[0][1] += delta[1] 
                        delta = self.roundPoint(csp[2])
                        csp[2][0] += delta[0] 
                        csp[2][1] += delta[1] 
            node.set('d', p.to_path())

    def style_round_it(self, node, name):
        if node.tag == inkex.addNS('g', 'svg'):
            for e in node:
                self.style_round_it(e)
        elif name in node.style:
            node.style[name] = self.roundUnit(node.style[name])

    def attribute_round_it(self, node, name):
        if node.tag == inkex.addNS('g', 'svg'):
            for e in node:
                self.attribute_round_it(e)
        else:
            value = node.get(name)
            if value:
                node.set(name, self.roundUnit(value))

    def effect(self):
        for node in self.svg.selected:
            if self.options.paths:
                self.path_round_it(node)
            if self.options.strokewidth:
                self.style_round_it(node, 'stroke-width')
            if self.options.widthheight:
                self.attribute_round_it(node, 'width')
                self.attribute_round_it(node, 'height')
            if self.options.position:
                self.attribute_round_it(node, 'x')
                self.attribute_round_it(node, 'y')
            if self.options.opacity:
                self.style_round_it(node, 'opacity')
            if self.options.strokeopacity:
                self.style_round_it(node, 'stroke-opacity')
            if self.options.fillopacity:
                self.style_round_it(node, 'fill-opacity')


if __name__ == '__main__':
    svgRounder().run()


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
