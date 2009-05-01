# -*- coding: utf-8 -*-
 #include "treeitem.h"
 
class TreeItem ():
  def __init__(self, data,parent) :
    self.parentItem = parent;
    self.itemData = data;

  def appendChild(item) :
    self childItems.append(item);
       
       TreeItem *TreeItem::child(int row)
       {
         return childItems.value(row);
         }
         
         int TreeItem::childCount() const
         {
           return childItems.count();
           }
           
           int TreeItem::columnCount() const
           {
             return itemData.count();
             }
             
             QVariant TreeItem::data(int column) const
             {
               return itemData.value(column);
               }
               
               TreeItem *TreeItem::parent()
               {
                 return parentItem;
                 }
                 
                 int TreeItem::row() const
                 {
                   if (parentItem)
                   return parentItem->childItems.indexOf(const_cast<TreeItem*>(this));
                   
                   return 0;
                   }