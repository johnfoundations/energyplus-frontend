# -*- coding: utf-8 -*-
"""***************************************************************************
*   Copyright (C) 2009 by Derek Kite   *
*   dkite@shaw.ca   *
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
*   This program is distributed in the hope that it will be useful,       *
*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
*   GNU General Public License for more details.                          *
*                                                                         *
*   You should have received a copy of the GNU General Public License     *
*   along with this program; if not, write to the                         *
*   Free Software Foundation, Inc.,                                       *
*   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
***************************************************************************"""


def ArrayChoice(array, default) :
  """array is list of items, default is index """
  count = -1
  array.each do |litem|
    count = count + 1
    if count == default
      puts count.to_s + '*  ' + litem
    else
      puts count.to_s + '   ' + litem


  STDOUT.flush
  sel = gets.chomp
  if sel == ''
    return array.at(default)
  end
  while sel.to_i < 0 && sel.to_i > count
    puts 'Selection out of range. Type a number from 0 - ' + count + 'or hit enter to select the default'
    STDOUT.flush
    sel = gets.chomp
    if sel == ''
      return array.at(default)
    end
  end
  return array.at(sel.to_i)
end
