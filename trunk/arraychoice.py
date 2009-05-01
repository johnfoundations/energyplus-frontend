# -*- coding: utf-8 -*-
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
