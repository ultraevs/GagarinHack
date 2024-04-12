import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  items: [],
  amount: 0,
};

export const filesSlice = createSlice({
  name: "files",
  initialState,
  reducers: {
    addOrUpdateItem: (state, action) => {
      const itemInArray = state.items.some((item) => {
        return item.img === action.payload.img;
      });

      if (!itemInArray) {
        state.items.push(action.payload.item);
        state.amount = state.items.length;
      } else {
        state.items.map((item) => {
          if (item.img === action.payload.img) {
            item.info = action.payload.info;
          }
          return item;
        });
      }
    },
  },
});

export const { addOrUpdateItem } = filesSlice.actions;

export default filesSlice.reducer;
