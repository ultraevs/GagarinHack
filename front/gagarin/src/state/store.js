import { configureStore } from "@reduxjs/toolkit";
import filesSlice from "./files/filesSlice";

const store = configureStore({
  reducer: {
    files: filesSlice,
  },
});

export default store

export const RootState = store.getState();
export const AppDispatch = store.dispatch;
