import { createSlice } from "@reduxjs/toolkit";
import nameEncoder from "../../utils/nameEncoder";

const initialState = {
  items: [],
  amount: 0,
};

export const filesSlice = createSlice({
  name: "files",
  initialState,
  reducers: {
    addOrUpdateItem: (state, action) => {
      const name = nameEncoder(action.payload.info.type, action.payload.info.page_number);

      const itemIndex = state.items.findIndex((item) => item.name === name);

      if (itemIndex === -1) {
        state.items.push({ ...action.payload, name: name });
        state.amount = state.items.length;
      } else {
        state.items = state.items.map((item, index) => {
            if (index === itemIndex) {
              return {
                ...item,
                info: action.payload.info,
                img: action.payload.img,
              };
            }
            return item;
          });
      }
    },
  },
});

export const { addOrUpdateItem } = filesSlice.actions;

export default filesSlice.reducer;
