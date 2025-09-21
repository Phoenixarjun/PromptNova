"use client"
import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface CardType {
  name: string;
  description: string;
}

export const CardDesign = ({type}: { type: CardType}) => {
  return (
    <Card className="bg-white border-gray-300 hover:border-gray-500 transition-colors cursor-pointer">
      <CardHeader>
        <CardTitle className="text-xl text-gray-800">{type.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-600 text-sm">{type.description}</p>
      </CardContent>
    </Card>
  )
}
