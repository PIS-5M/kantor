import React from "react";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getFacetedMinMaxValues,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getFilteredRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { Button, Table } from "reactstrap";
import { Filter } from "./table-utils";
const columnHelper = createColumnHelper();

const columns = [
  columnHelper.accessor("publication_date", {
    header: "Data wystawienia",
    cell: ({ getValue }) => getValue().toLocaleString(),
    enableColumnFilter: false,
  }),
  columnHelper.accessor("last_modification_date", {
    header: "Data modyfikacji",
    cell: ({ getValue }) => getValue().toLocaleString(),
    enableColumnFilter: false,
  }),
  columnHelper.accessor("value", {
    header: "Kwota",
  }),
  columnHelper.accessor("exchange_rate", {
    header: "Cena",
  }),
  columnHelper.accessor("currency", {
    header: "Waluta",
  }),
  columnHelper.accessor("wanted_currency", {
    header: "Poszukiwana waluta",
  }),
  columnHelper.display({
    header: "",
    id: "buy",
    cell: ({ row }) => (
      <Button className="bg-blue-600 hover:bg-blue-600/90">Kup ofertę</Button>
    ),
  }),
];

export const AllOffersTable = ({ data }) => {
  const [columnFilters, setColumnFilters] = React.useState([]);
  const table = useReactTable({
    data,
    columns,
    state: {
      columnFilters,
    },
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getFacetedMinMaxValues: getFacetedMinMaxValues(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
  });
  return (
    <Table className="custom-table">
      <thead className="!bg-blue-600 !text-white text-center ">
        {table.getHeaderGroups().map((headerGroup) => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <th key={header.id} colSpan={header.colSpan}>
                {flexRender(
                  header.column.columnDef.header,
                  header.getContext()
                )}
                {header.column.getCanFilter() ? (
                  <div className="text-black">
                    <Filter column={header.column} table={table} />
                  </div>
                ) : null}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map((row) => {
          return (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => {
                return (
                  <td className="text-center" key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                );
              })}
            </tr>
          );
        })}
      </tbody>
    </Table>
  );
};
