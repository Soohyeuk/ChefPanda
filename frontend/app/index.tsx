import { Link } from "expo-router";
import React, { useState } from "react";
import { Button, Pressable, Text, View } from "react-native";

export default function Index() {
  const [count, setCount] = useState(0);

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>Hi</Text>
      <Text>{count}</Text>
      <Button title="Click me" onPress={() => setCount(count + 1)} />
      

      <Link href="/about" asChild>
        <Pressable>
          <Text style={{ color: "blue" }}>Go to About</Text>
        </Pressable>
      </Link>
    </View>
  );
}
