import React, { useEffect, useState } from "react";
import BlogList from "../components/BlogList";
import Pagination from "../components/Pagination";
import { BlogService } from "../api/services.gen";
import { BlogPost } from "../api/types.gen";


const Blog = () => {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [count, setCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrevious, setHasPrevious] = useState(false);
  const pageSize= 6;

  useEffect(() => {
	  setLoading(true);
	  setError(null);

	  BlogService.blogList({ page: currentPage })
		.then((data) => {
		  setPosts(data.results);
		  setHasNext(Boolean(data.next));
		  setHasPrevious(Boolean(data.previous));
		  setCount(data.count);
		})
		.catch(() => setError("Erro ao buscar posts"))
		.finally(() => setLoading(false));
  }, [currentPage]);

  return (
    <>
    <h2 className="my-4 text-center mb-5 mt-2">Publicações Recentes</h2>
    <BlogList posts={posts} loading={loading} error={error} />
    <Pagination currentPage={currentPage} pageSize={pageSize} count={count} hasNext={hasNext} hasPrevious={hasPrevious} onPageChange={setCurrentPage} />
    </>
 )
};

export default Blog;

