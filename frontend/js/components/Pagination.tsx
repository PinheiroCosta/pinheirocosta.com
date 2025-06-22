interface PaginationProps {
    currentPage: number;
    hasNext: boolean;
    hasPrevious: boolean;
    pageSize: number;
    count: number;
    onPageChange: (page: number) => void;
}


const Pagination: React.FC<PaginationProps> = ({ currentPage, hasNext, hasPrevious, pageSize, count, onPageChange }) => {
    const totalPages = Math.ceil(count / pageSize);
    return (
        <div className="pagination-container d-flex justify-content-center space-x-2 mt-4">
            {/* Botão Anterior */}
            <button 
                onClick={() => onPageChange(currentPage -1)}
                disabled={!hasPrevious}
                className="btn btn-primary px-3 py-1 rounded disabled:opacity-50"
            >
            {"⤺"}
            </button>

            {/* Números das Páginas */}
            <span className="px-3 py-1">{`Página ${currentPage} de ${totalPages} `}</span>
            
            {/* Botão Próximo */}
            <button
                onClick={() => onPageChange(currentPage + 1)}
                disabled={!hasNext}
                className="btn btn-primary px-3 py-1 rounded disabled:opacity-50"
            >
                {"⤻"}
            </button>
        </div>
    );
};

export default Pagination;
